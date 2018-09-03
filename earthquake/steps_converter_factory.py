from earthquake.steps_converter import StepsConverter, DelegateDeltaStepsConverter, DelegateAngularStepsConverter, \
    ScalingDelegateStepsConverter, StepperStepsConverter


def create_for_step_motor(
        step_time: float, scale_factor,
        radius: float) -> StepsConverter:
    return \
        DelegateDeltaStepsConverter(
            DelegateAngularStepsConverter(
                ScalingDelegateStepsConverter(
                    StepperStepsConverter(step_time),
                    scale_factor
                ),
                radius
            )
        )
