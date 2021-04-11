# Dataset

### [Kaggle link](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks/)

- `data.csv`: This csv file contains the data mentioned in the description. Each row represents a single track, each column represents a field of the track (audio features and identifiers).
- `data_by_artist.csv`: This file contains the audio features of each artist, resulted from the aggregation. The rows represent different artists, columns represent different audio features.
- `data_by_genres.csv`: This file contains the audio features of each genre. The rows represent different genres, and the columns represent different audio features..
- `data_by_year.csv`: This data file contains the track data grouped by the year of release of each track, and allows time-series operations to be performed. Each row represents a single year, each column represents an audio feature. The bias of data is as minimal as possible.
- `data_w_genres.cav`: This file is an extension to the "data_by_artist.csv" file with genres implementation for each artist. Each row represents a single artist, each column represents an audio feature.
- `data_merged.csv`: The merged dataset file that we formed after data preprocessing and feature engineering as described briefly in our report. 
