# summer2017_polisci

3. Political science summer project

The project here is most of the code I wrote this summer as a side project
working with a polisci / environmental policy graduate student. Part of her
thesis examined whether politicians nearing critical times like their re-election
cycle would spend more time talking about certain "desirable" topics -- in this
case topics regarding the environment. I joined her to figure out a way to use
programming to help her research. We decided to approach this problem by
building a tool that would allow her to visualize the frequency governors spoke
about certain topics over time. You can skip the rest of the reading and view
the final result by opening the demo.html at data_vis/plots. :)

To do this, I had to scrape governors' speeches from a website called
votesmart.org that keeps track of speeches, votes, positions, bios, etc for
a variety of politicians. I used Selenium as my scraping tool, and a lot of this
was nitty-gritty parsing and examining HTML. In the end I had a corpus of
speeches for current and past governors. The next primary part of this project
was using plotly to generate an intuitive line graph for represent the data.
The simple version requires the user to input a list of keywords to represent
the "topics" to search for by frequency. The plot would show the relative and
raw frequencies of these topics across time for each governor.

To run, navigate to the summer2017_polisci directory and run
"pip install -r requirements.txt" to download all the necessary requirements.
You may have to download pip if you don't already have it.
Then, modify the list of keywords to search for on line 17 in the INPUTS section
of frequency_analysis/percentage_keyword_speech.py. Now run
"python percentage_keyword_speech.py" to generate the frequency count csv.
Lastly, you can see the plot by running "python plot.py" in the data_vis
directory. Also, I realize this should be combined into one script, but I
just hadn't gotten around to that yet, many apologies!

Extras:
- I've included the full results of the scraper already in this project, but
if you wish to see the scraper in action you can delete the content inside
votesmart_scraper/outputs/current_governors and then run
"python selenium_votesmart_scraper.py". It *should* still run on your machine.
- A natural language processing branch: instead of having the user manually
input topics, I wanted to be able to analyze the corpus using latent dirichlet
allocation (LDA), which generates a probabilistic model that can be used to
infer most likely "topics". A layman's explanation can be found here:
http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
And a much more in-depth paper (that I don't understand fully) can be found here:
http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf
By the end of the summer I got this to run but not well enough to have
clean or useful topics. However, you can see it in action if you run
"python lda_models.py". You can also see some preprocessing as well in
"preprocessing.py" that includes some stemming and filtering of stop words.
- There are some other files I used to interact with dropbox in the
dropbox_utils folder. One fun shell script that I figured out can be used
to unzip all the zip files within a folder into new folders with the same name
as the original zip file.
