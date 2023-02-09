# offsettmpsubs

A cli tool for delaying/hastening subtitles in stored in TMP format.

## Installation

```
$ pip install --user offsettmpsubs
```

## Usage

```
$ offsettmpsubs --help
usage: offsettmpsubs [-h] OFFSET INFILE OUTFILE

Delay or hasten subtitles in MTP format.

positional arguments:
  OFFSET      amount of time, by which the timestamps in the output file
              should be delayed (if negative) or hasten. Examples of allowed
              values: "10" (delay by ten seconds), "-10", "+10", "-01:00"
              (hasten by one minute), "01:00:00" (delay by one hour)
  INFILE      file name of the original subtitle file
  OUTFILE     file name of the new file with delayed/hastened subtitles

options:
  -h, --help  show this help message and exit
$ head s05e09_subs_en.txt
00:00:02:Here are our final actual costs for this year.
00:00:05:Okay.
00:00:06:As you can see, we did pretty well, so...
00:00:08:Yes. Yes, I can see
00:00:11:that we did indeed.
00:00:14:Why don't you explain this to me|like I am an eight-year-old?
00:00:17:All right, well, this is the overall|budget for this fiscal year
00:00:21:along the X axis.
00:00:24:Yes. There's the X axix.|Right there.
00:00:26:You can see clearly on this page|that we have a surplus
$ offsettmpsubs 01:23 s05e09_subs_en.txt delayed.txt
$ head delayed.txt
00:01:25:Here are our final actual costs for this year.
00:01:28:Okay.
00:01:29:As you can see, we did pretty well, so...
00:01:31:Yes. Yes, I can see
00:01:34:that we did indeed.
00:01:37:Why don't you explain this to me|like I am an eight-year-old?
00:01:40:All right, well, this is the overall|budget for this fiscal year
00:01:44:along the X axis.
00:01:47:Yes. There's the X axix.|Right there.
00:01:49:You can see clearly on this page|that we have a surplus
```
