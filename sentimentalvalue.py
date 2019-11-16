import re
import pandas as pd

## dictionary to hold hashtags and their sentimental value
dictHashTags = []
## parse the dates of tweets
data = pd.read_csv("tweets.csv", parse_dates=['timestamp'])

hash_tag_retrieval = data.iloc[:, -1]
hash_tag_retrieval = hash_tag_retrieval.to_string()
group = re.findall(r"#(\w+)", hash_tag_retrieval)

dictHashTags = dict.fromkeys(group, )

new_df = data.set_index(['timestamp']).sort_index()

##
##data = data.reset_index().set_index('timestamp')
##new_df = data.resample("T")
print(new_df)