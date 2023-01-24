# Conference Deadlines

Countdown timers to keep track of a bunch of CV/NLP/ML/RO conference deadlines available
at [https://deadlines.info](https://deadlines.info).

This is a [fork][2] with the following changes:

- add calendar overview for deadlines and conference dates (see [here](https://deadlines.info/calendar))
- some design changes, e.g.
  - add direct link to conference website with Icons from [IcoMoon](https://icomoon.io/#icons-icomoon)
  - add display of h-index and display of full conference name on hover (inspiration from [ad-deadlines.com][13])
  - add display of conference ranking

## Contributing

Contributions are very welcome!

To add or update a deadline:

- Fork the repository (you can also press `.` to open this repo in VS Code in your browser)
- Update [`_data/conferences.csv`](_data/conferences.csv) (best done with MS Excel or similar)
- Make sure it has the `title`, `year`, `id`, `link`, `deadline`, `timezone`, `date`, `place`, `sub` attributes
  - See available timezone strings [here](https://momentjs.com/timezone/).
- Optionally add a `note` and `abstract_deadline` in case the conference has a separate mandatory abstract deadline
- Optionally add `hindex` (refers to h5-index from [here](https://scholar.google.com/citations?view_op=top_venues&vq=eng))
- Optionally add `hindex` (refers to h5-index
  from [Google](https://scholar.google.com/citations?view_op=top_venues&vq=eng)) or [Guide2Research](https://research.com/conference-rankings/computer-science/2021/machine-learning)
- Optionally add `ranking` from [conference ranks](http://www.conferenceranks.com/)
- sort data ascending by deadline
- Example:
    ```yaml
    - title: BestConf
      year: 2022
      id: bestconf22  # title as lower case + last two digits of year
      full_name: Best Conference for Anything  # full conference name
      link: link-to-website.com
      deadline: YYYY-MM-DD HH:MM
      abstract_deadline: YYYY-MM-DD HH:MM
      timezone: Asia/Seoul
      place: Incheon, South Korea
      date: September, 18-22, 2022
      start: YYYY-MM-DD
      end: YYYY-MM-DD
      paperslink: link-to-full-paper-list.com
      pwclink: link-to-papers-with-code.com
      hindex: 100.0
      sub: SP
      note: Important
    ```
- Send a pull request

## Usage

### Host own website

- fork the repo
- adjust [`_config.yml`](_config.yml) with your URLs
  ```yaml
  domain: "https://<user-name>.github.io/"
  baseurl: "/<repo-name>"
  ```
- remove [`CNAME`](CNAME)
- adjust or remove [Impressum](impressum.html)
- adjust the [`_data/conferences.csv`](_data/conferences.csv)
- if you want a domain different from Github, check [this](https://dafero.wordpress.com/2020/02/19/how-to-configure-github-pages-with-a-custom-ionos-old-11-domain/)

### Locally

To test/develop the site locally with Docker:

- Run
  ```shell
  docker run --mount type=bind,source=${PWD},target=/srv/jekyll -p 4000:4000 -it --rm --name conference-deadlines jekyll/jekyll:3.8 jekyll serve
  # with live reload
  docker run --mount type=bind,source=${PWD},target=/srv/jekyll -p 4000:4000 -it --rm --name conference-deadlines jekyll/jekyll:3.8 jekyll serve --incremental --livereload --force_polling
  ```

## License

Unless otherwise stated, this work is licensed under the [MIT](LICENSE) license
- Based on [AI Deadlines](https://github.com/abhshkdz/ai-deadlines): [MIT][1]
- Using [IcoMoon Icons](https://icomoon.io/#icons-icomoon): [GPL](http://www.gnu.org/licenses/gpl.html) / [CC BY4.0](http://creativecommons.org/licenses/by/4.0/)
- Using Deadline information from [WikiCFP](http://wikicfp.com/cfp/) with [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/), thus all information in [_data](_data) falls under this license
- Using ranking information from [CORE](http://portal.core.edu.au/conf-ranks/)

[1]: https://abhshkdz.mit-license.org/
[2]: http://aideadlin.es/
[13]: https://ad-deadlines.com/
