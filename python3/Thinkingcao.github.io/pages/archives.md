---
layout: page
title: All articles are here
titlebar: archives
subtitle: <span class="mega-octicon octicon-calendar"></span>&nbsp;&nbsp;专题系列： &nbsp;&nbsp; <a href ="http://www.ityouknow.com/arch.html"><font color="#1A0DAB">架构</font></a>&nbsp;&nbsp; <a href ="http://www.ityouknow.com/life.html"><font color="#EB9439">故事</font></a>&nbsp;&nbsp; <a href ="http://www.ityouknow.com/docker.html"><font color="#1E90FF">Docker</font></a>
menu: archives
css: ['blog-page.css']
permalink: /archives.html
---

<ul class="archives-list">
  {% for post in site.posts %}

    {% unless post.next %}
      <h3>{{ post.date | date: '%Y' }}</h3>
    {% else %}
      {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
      {% capture nyear %}{{ post.next.date | date: '%Y' }}{% endcapture %}
      {% if year != nyear %}
        <h3>{{ post.date | date: '%Y' }}</h3>
      {% endif %}
    {% endunless %}

    <li><span>{{ post.date | date:'%m-%d' }}</span> <a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>