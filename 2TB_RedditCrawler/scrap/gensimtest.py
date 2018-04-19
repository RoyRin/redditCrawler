import gensim
import random
from gensim.models import Word2Vec, KeyedVectors
import json
import re
import os
import glob
import sys

model = Word2Vec(size=25, window=8, min_count=1, workers=4)
model.save("/Users/Roy/Research/BudMishra/redditCrawler/2TB_RedditCrawler/scrap/W2Vtest2.txt")