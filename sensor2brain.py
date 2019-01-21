@nrp.MapSpikeSource("input_2", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("input_1", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("input_0", nrp.brain.sensors[0], nrp.dc_source)
@nrp.Robot2Neuron()
def sensor2brain(t, input_2, input_1, input_0):
    import rospy
    from std_msgs.msg import Int32

    input_0.amplitude = 1.0
    input_1.amplitude = 1.0
    input_2.amplitude = 1.0