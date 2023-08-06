from bookRecommender import __version__ as _version
from bookRecommender.config.core import config
from bookRecommender.processing.data_manager import load_pipeline
from bookRecommender.train_pipeline import run_training

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
book_pipe = load_pipeline(file_name=pipeline_file_name)

"input_data -> book_name, return -> Books that similar to queried book"


def make_prediction(
    input_data: str,
) -> list:
    """Make a prediction using a saved model pipeline."""

    if book_pipe is None:
        run_training()
        pipe = load_pipeline(file_name=pipeline_file_name)
    else:
        pipe = book_pipe

    results = []
    matrix = pipe.named_steps["prepare"].get_prepared_data()
    try:
        distances, indices = pipe.named_steps["knn"].kneighbors(
            matrix.loc[input_data, :].values.reshape(1, -1),
            n_neighbors=config.model_config.num_neighbors
        )
    except KeyError:
        return ["No such book found. Nothing to recommend :("]

    for i in range(0, len(distances.flatten())):
        if i == 0:
            results.append("Recommendations for {0}:\n".format(
                matrix.loc[input_data, :].name))
        else:
            results.append(
                "{0}: {1}, with distance of {2}:".format(
                    i, 
                    matrix.index[indices.flatten()[i]],
                    distances.flatten()[i]
                )
            )

    return results
