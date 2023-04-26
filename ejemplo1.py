from manim import *
import itertools as it
class Cuerpo(VMobject):
    CONFIG={
        'first_zero': 0,
        'max_ratio_shown': .1,
        'frequency': .2,
        'use_copy': True
    }
    def __init__(self, template, random_freq, **kwargs):
        VMobject.__init__(self, **kwargs)
        if self.CONFIG['use_copy'] is False:
            self.ghost_mob = template.copy().fade(1)
            self.add(self.ghost_mob)
        else:
            self.ghost_mob = template.copy()
        self.shown_mob = template.copy()
        self.shown_mob.random_freq=random_freq
        self.shown_mob.clear_updaters()
        self.add(self.shown_mob)
        def update(mob, dt):
            mob.CONFIG['first_zero'] += dt
            period = 1/mob.CONFIG['frequency']
            unsmooth_alpha = (mob.CONFIG['first_zero'] % period)/period
            alpha = unsmooth_alpha
            mrs = mob.CONFIG['max_ratio_shown']
            mob.shown_mob.pointwise_become_partial(
                mob.ghost_mob,
                max(interpolate(-mrs, 1, alpha/10*mob.shown_mob.random_freq), 0),
                min(interpolate(0, 1+mrs, alpha/10*mob.shown_mob.random_freq), 1)
            )
        self.add_updater(update)
class MakingScene(Scene):
    CONFIG={
        'colors': [
            RED, GREEN, BLUE, YELLOW
        ]
    }
    def construct(self):
        radios=[.25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
        arcs=VGroup()
        my_color=it.cycle(self.CONFIG['colors'])
        for radio in radios:
            arc=Arc(start_angle=0, angle=2*PI, radius=radio, stroke_width=15)
            arc.set_color(color=next(my_color))
            my_intent=Cuerpo(arc,np.random.random())
            arcs.add(my_intent)
        self.add(arcs)
        self.wait(10)