
# `stravamous`

`stravamous` is my attempt to anonymize running or cycling GPS tracks that are going
to be uploaded to http://strava.com.

Strava does have a feature to hide the first 500 - 1000m
of your ride. This has the following disadvantages:

+ It removes some of the distance of your ride. You might not like that.
+ It is possible, with enough data, to get a good idea on where you might live.
+ You have to give your/an address to Strava. I prefer not to give out that information.

## Features

+ You can predefine a `splice` segment that will get spliced into your track, thereby obfuscating your
  true starting position.
+ (Future) The time of your ride can be adjusted by a random amount in case you don't want someone
  to know that you and your nice bike always pass a certain corner around 2:35PM every day.

## Requirements

+ This is designed for running under Mac OS X. I imagine certain portions of it can be made to work
  on other operating systems.
+ You need to download `GPSBabel` (a great piece of software for converting GPS output to many different
  formats)
+ You need to install a pip module called configurati. I'll make this a package requirement in the future.

## Notes

I haven't done much on this and it barely works for my immediate needs. That will change depending
on how much time I decide to put into this and how many others might be using it. Drop me a note if
you want to use this and have feature requests so I can help prioritize my efforts.

