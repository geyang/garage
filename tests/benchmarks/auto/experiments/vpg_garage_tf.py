"""A regression test for automatic benchmarking garage-TensorFlow-VPG."""
import gym
import tensorflow as tf

from garage import wrap_experiment
from garage.envs import normalize
from garage.experiment import deterministic
from garage.np.baselines import LinearFeatureBaseline
from garage.tf.algos import VPG as TF_VPG
from garage.tf.envs import TfEnv
from garage.tf.experiment import LocalTFRunner
from garage.tf.policies import GaussianMLPPolicy2 as TF_GMP

hyper_parameters = {
    'hidden_sizes': [64, 64],
    'center_adv': True,
    'learning_rate': 1e-2,
    'discount': 0.99,
    'n_epochs': 250,
    'max_path_length': 100,
    'batch_size': 2048,
}


@wrap_experiment
def vpg_garage_tf(ctxt, env_id, seed):
    """Create garage TensorFlow VPG model and training.

    Args:
        ctxt (garage.experiment.ExperimentContext): The experiment
            configuration used by LocalRunner to create the
            snapshotter.
        env_id (str): Environment id of the task.
        seed (int): Random positive integer for the trial.

    """
    deterministic.set_seed(seed)

    with LocalTFRunner(ctxt) as runner:
        env = TfEnv(normalize(gym.make(env_id)))

        policy = TF_GMP(
            env_spec=env.spec,
            hidden_sizes=hyper_parameters['hidden_sizes'],
            hidden_nonlinearity=tf.nn.tanh,
            output_nonlinearity=None,
        )

        baseline = LinearFeatureBaseline(env_spec=env.spec)

        algo = TF_VPG(env_spec=env.spec,
                      policy=policy,
                      baseline=baseline,
                      max_path_length=hyper_parameters['max_path_length'],
                      discount=hyper_parameters['discount'],
                      center_adv=hyper_parameters['center_adv'],
                      optimizer_args=dict(tf_optimizer_args=dict(
                          learning_rate=hyper_parameters['learning_rate']),
                                          verbose=True))

        runner.setup(algo, env)
        runner.train(n_epochs=hyper_parameters['n_epochs'],
                     batch_size=hyper_parameters['batch_size'])