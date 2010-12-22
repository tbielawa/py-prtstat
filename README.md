# PY-PRT #

Analyzes tweets in Morgantown to estimate the status of
the Morgantown People Mover (PRT).

## Concept ##
[West Virginia University](http://wvu.edu) is a college that spans three (or
perhaps four) campuses separated geographically. In 1972 the university created
a transit system, the PRT. PRT stands for Personal Rapid Transit (which many
believe is neither personal, nor rapid).

Unfortunately, the PRT is prone to failure. In addition, these failures seem to
happen frequently and randomly. The PRT staff have began adopting technology
for alerting students of outages, but often the best way to see if the PRT is
operational is to walk to the station and find out.

Since students tend to be more social-media aware, and write about all aspects
of their lives, we're banking on Twitter being a responsive way to make a guess
on the PRTs status. This project is an experiment on data-mining Twitter using
a variety of techniques to best describe the status of the PRT. Hopefully we'll
have something neat at the end, but more importantly, we're here to learn and
play.

## Details ##
py-prt is written in Python. It uses the Twitter search API to provide JSON
search results for the Morgantown area. It also pulls in weather data for
Morgantown, WV using a Yahoo! XML feed. For the most part, at least right now,
it doesn't DO anything with that weather data, but hey, we're getting there.

## Contributors ##
Tim 'Shaggy' Bielawa [mail](mailto:timbielawa@gmail.com)|[web](https://github.com/tbielawa)  
Andrew Butcher [mail](mailto:abutcher@afrolegs.com)|[web](http://afrolegs.com)  
Ricky Hussmann [mail](mailto:ricky.hussmann@gmail.com)|[web](http://rhussmann.com)  
Kel Cecil kelcecil -at- praisechaos -dot- com|[github](http://github.com/kelcecil)|[web](http://www.praisechaos.com)
