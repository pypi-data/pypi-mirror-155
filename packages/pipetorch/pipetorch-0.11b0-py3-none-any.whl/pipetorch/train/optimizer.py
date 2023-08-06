import optuna
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np

class Optimizer(optuna.study.Study):
    def __init__(self, study, targets):
        super().__init__(study.study_name, study._storage, study.sampler, study.pruner)
        self.targets = targets if isinstance(targets, list) else [targets]
        
    @classmethod
    def create_study(cls, targets='loss', storage=None, sampler=None, pruner=None, study_name=None, direction=None, load_if_exists=False, directions=None):
        if type(targets) == list and len(targets) > 1 and directions is None:
            directions = ['minimize'] + ['maximize'] * (len(targets)-1)
        study = optuna.create_study(storage=storage, sampler=sampler, pruner=pruner,
                                         study_name=study_name, direction=direction, load_if_exists=load_if_exists, directions=directions)
        return cls(study, targets)

    def filter_targets(self, results):
        return [ results[t] for t in self.targets ]
    
    def sweeps(self):
        for t in self.trials:
            try:
                sweeps
            except:
                sweeps = {param:{ target:[] for target in self.targets } for param in t.params }
            for param, paramv in t.params.items():
                for target, value in zip(self.targets, t.values):
                    sweeps[param][target].append((paramv, value))
        return { param:{t:np.array(sorted(l)) for t, l in target.items() } for param, target in sweeps.items()}
    
    def distribution(self, param):
        dist = self.trials[0].distributions[param]
        return dist
    
    def is_log_distribution(self, param):
        return self.distribution(param).__class__.__name__.startswith('Log')
    
    def plot_hyperparameters(self, figsize=None):
        sweeps = self.sweeps()
        if figsize is None:
            figsize = (2 * len(self.targets), 2 * len(self.trials[0].distributions))
        fig, axs = plt.subplots(len(self.targets), len(sweeps), sharex='col', sharey='row', figsize=figsize)
        
        if len(sweeps) == 1:
            if len(self.targets) == 1:
                axs = np.array([[axs]])
            else:
                axs = np.expand_dims(axs, axis=1)
        elif len(self.targets) == 1:
            axs = np.expand_dims(axs, axis=0)
        for parami, param in enumerate(sweeps):
            for targeti, target in enumerate(sweeps[param]):
                self._subplot(axs[targeti, parami], sweeps[param][target])
                if targeti == 0:
                    axs[targeti, parami].set_title(param)
                    if self.is_log_distribution(param):
                        axs[targeti, parami].set_xscale('log')
                if parami == 0:
                    axs[targeti, parami].set_ylabel(target)
        return fig
    
    def _subplot(self, ax, z):
        x = z[:, :1]
        y = z[:, 1]
        poly = PolynomialFeatures(degree=3)
        xt = poly.fit_transform(x)
        model = LinearRegression()
        model.fit(xt, y)
        ax.scatter(x, y)
        yp = model.predict(xt)
        ax.plot(x, yp, c='red')
        
    def plot(self):
        optuna.visualization.plot_slice(self, params=["hidden"],
                                  target_name="F1 Score")
    
            
