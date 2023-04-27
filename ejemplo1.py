from manim import *
class StartTemplate(VMobject):
    CONFIG={
        'start_time': 0,
        'frequency': .1,
        'max_ratio_shown': .5,
        'use_copy': True
    }
    def __init__(self, template, rand_freq,**kwargs):
        VMobject.__init__(self, **kwargs)
        if self.CONFIG['use_copy']:
            self.ghost_mob = template.copy().fade(1)
            self.add(self.ghost_mob)
        else:
            self.ghost_mob = template
        self.shown_mob = template.copy()
        self.shown_mob.clear_updaters()
        self.rand_freq = rand_freq
        self.add(self.shown_mob)
        self.total_time = self.CONFIG['start_time']
        def update(mob, dt):
            mob.total_time += dt
            period = 1/mob.CONFIG['frequency']
            # es importante la / para que el moviemietno de los hases sea perpetuo
            unsmooth_alpha = (mob.total_time % period)/period
            alpha = unsmooth_alpha  # aca no puse el bezier 
            mob.shown_mob.pointwise_become_partial(
                mob.ghost_mob,
                # que pasa si saco el maximo?
                1.5*alpha-.4,
                1.5*alpha
            )
        self.add_updater(update)
class Curves(VMobject):
    CONFIG={
        'frequency': .2,
        'max_ratio_shown': .3,
        'n_end': 2,
        'n_layers': 10,
        'radius': 1,
        'colors': [YELLOW_A, YELLOW_E],
        'R': 5,
        'r': 3,
        'd': 5,
    }
    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        lines = self.get_lines()
        self.add(*[StartTemplate(line, np.random.random())
            for line in lines
        ])
        self.randomize_times()
    def randomize_times(self):
        for submob in self.submobjects:
            if hasattr(submob, 'total_time'):
                T = 1/submob.CONFIG['frequency']
                submob.total_time = T*np.random.random()
    def get_lines(self):
        a=.2
        return VGroup(*[
            self.get_line(
                self.CONFIG['radius']*(
                    1-a+2*a*np.random.random()
                )
            ) for x in range(self.CONFIG['n_layers'])
        ])
    def get_line(self,r):
        return ParametricFunction(
            lambda t: np.array([
                r*np.cos(2*np.pi*t),
                r*np.sin(2*np.pi*t),
                0
            ]),
            t_range=[0, 1]
        )
class EffectScene(Scene):
    def construct(self):
        effect_curves=Curves().set_height(config['frame_height'])
        self.add(effect_curves)
        self.wait(15)