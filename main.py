import server.ml.data as data_module
import server.ml.baselines as baselines
from server.ml.training import run_model_building

MODEL_TRAINING = False

def main():

    if MODEL_TRAINING:
        data_module.main()
        baselines.main()
        run_model_building()

    


if __name__ == "__main__":
    main()
