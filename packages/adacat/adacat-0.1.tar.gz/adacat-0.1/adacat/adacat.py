
import torch
from torch.distributions import Distribution, constraints, Normal
from torch.distributions.utils import broadcast_all
import torch.nn.functional as F

class Adacat(Distribution):
    arg_constraints = {'logits': constraints.real}
    support = constraints.unit_interval

    @property
    def mean(self):
        return ((self.x_cum - self.x_sizes / 2.) * self.y_sizes).sum(dim=-1)

    @property
    def x_sizes(self):
        return F.softmax(self.x_logits, dim=-1)

    @property
    def x_cum(self):
        return torch.cumsum(self.x_sizes, dim=-1)
    
    @property
    def y_sizes(self):
        return F.softmax(self.y_logits, dim=-1)
    
    @property
    def y_cum(self):
        return torch.cumsum(self.y_sizes, dim=-1)
    
    @property
    def log_x_sizes(self):
        return F.log_softmax(self.x_logits, dim=-1)
    
    @property
    def log_y_sizes(self):
        return F.log_softmax(self.y_logits, dim=-1)

    def __init__(self, logits, validate_args=None):
        self.logits = logits
        assert logits.size(-1) % 2 == 0
        self.n_knobs = logits.size(-1) // 2
        self.x_logits, self.y_logits = logits.split(self.n_knobs, dim=-1)

        batch_shape = self.x_logits.size()[:-1]
        super(Adacat, self).__init__(batch_shape, validate_args=validate_args)

    def expand(self, batch_shape, _instance=None):
        new = self._get_checked_instance(Adacat, _instance)
        batch_shape = torch.Size(batch_shape)
        new.x_logits = self.x_logits.expand(batch_shape + (self.n_knobs,))
        new.y_logits = self.y_logits.expand(batch_shape + (self.n_knobs,))
        super(Adacat, new).__init__(batch_shape, validate_args=False)
        new._validate_args = self._validate_args
        return new

    def sample(self, sample_shape=torch.Size()):
        if not isinstance(sample_shape, torch.Size):
            sample_shape = torch.Size(sample_shape)

        batch_shape = self.y_sizes.shape[:-1]
        y_probs = self.y_sizes.reshape(-1, self.n_knobs)
        
        indices = torch.multinomial(y_probs, sample_shape.numel(), True).view(*batch_shape, sample_shape.numel())

        x_right = torch.gather(self.x_cum, -1, indices)
        x_size = torch.gather(self.x_sizes, -1, indices)
        x = x_right - x_size * torch.rand_like(x_size)

        return x.view(-1, sample_shape.numel()).t().view(*sample_shape, *batch_shape).contiguous()

    def log_prob(self, value, smooth_coeff=0.):
        
        x_cum, log_y_sizes, log_x_sizes, value = broadcast_all(self.x_cum, self.log_y_sizes, self.log_x_sizes, value.unsqueeze(-1))

        if smooth_coeff > 0.:
            value = torch.cat([value, value[..., :1]], dim=-1)

            # gaussian smooth kernel
            smd = Normal(loc=value, scale=torch.ones_like(value) * smooth_coeff)
            l = smd.cdf(torch.zeros_like(value))
            r = smd.cdf(torch.ones_like(value))
            log_z = (r - l).log()

            # analytically compute the integral
            x_cum = F.pad(x_cum, (1, 0))
            cdfs = smd.cdf(x_cum.clamp(min=0., max=1.))
            ws = (cdfs[..., 1:] - cdfs[..., :-1]) / (r[..., :-1] - l[..., :-1])

            return (ws * (log_y_sizes - log_x_sizes)).sum(dim=-1)
        
        else:
            
            value = value[..., :1]
            indices = torch.searchsorted(x_cum.contiguous(), value).clamp(0, self.n_knobs-1)

            log_x_size = torch.gather(log_x_sizes, -1, indices)
            log_y_size = torch.gather(log_y_sizes, -1, indices)

            return (log_y_size - log_x_size).squeeze(-1)

