from bookRecommender.config.core import config
from bookRecommender.pipeline import book_pipe
from bookRecommender.processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(
        file_name_book=config.app_config.data_file_book,
        file_name_user=config.app_config.data_file_user,
        file_name_rating=config.app_config.data_file_ratings,
    )

    # fit model
    book_pipe.fit(data)

    # persist trained model
    save_pipeline(pipeline_to_persist=book_pipe)


if __name__ == "__main__":
    run_training()
    print("trained")
