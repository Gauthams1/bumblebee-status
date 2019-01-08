# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs.

Parameters:
    * cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
    * cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
    * cpu.format  : Format string (defaults to "{:.01f}%)")
"""
 
try:
    import psutil
    import i3ipc
except ImportError:
    pass

import bumblebee.input
import bumblebee.output
import bumblebee.engine
class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.utilization)
        super(Module, self).__init__(engine, config, widget)
        widget.set("theme.minwidth", self._format.format(10.0-10e-20))
        self._utilization = "nothing"
        self._range = "Mb"
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd="gnome-system-monitor")

    @property
    def _format(self):
        return self.parameter("format", "{:.01f}Gb")

    def utilization(self, _):
        return self.parameter("format", "{:.01f} {} {} ").format(self._utilization,self._range,i3ipc.Connection().get_tree().find_focused().window_class)

    def update(self, widgets):
        ls=0
        updateparam=i3ipc.Connection().get_tree().find_focused().window_class
        for p in psutil.process_iter(attrs=['name','memory_info']):
            if (updateparam.lower().find(p.info['name']) != -1):
                ls+=(p.info['memory_info'].rss)
        if ls/(1024*1024) < 1024:        
            self._utilization = ls/(1024*1024)
            self._range = "Mb"
        else:
            self._utilization = ls/(1024*1024*1024)
            self._range = "Gb"

    def state(self, _):
        if self._range == "Gb":
            return self.threshold_state(self._utilization, 2, 3)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
