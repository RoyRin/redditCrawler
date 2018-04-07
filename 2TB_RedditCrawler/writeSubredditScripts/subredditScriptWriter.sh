#!/bin/bash
#SBATCH --job-name=redditCrawler
#SBATCH --nodes=2
#SBATCH --cpus-per-task= 25
#SBATCH --mem=10Gb
#SBATCH --time=60:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=rr2635@nyu.edu


for filename in /beegfs/avt237/data/RC* ; do
	srun --ntasks=1 --cpus-per-task=1 --exclusive --mem=10Gb python subredditScriptWriter.py "$filename" 
done

wait

##/beegfs/avt237/data/redditCrawler/2TB_RedditCrawler/writeSubredditScripts