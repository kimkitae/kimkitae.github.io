---
layout: page
lang: en
title: English archive
permalink: /en/
---

<p>
  Field notes on automation, testing, and AX, published in English.
  <a href="{{ '/' | relative_url }}">한국어 홈</a> ·
  <a href="{{ '/contact/' | relative_url }}">연락처</a>
</p>

{% assign english_posts = site.pages
  | where_exp: 'p', "p.url contains '/en/posts/'"
  | where_exp: 'p', 'p.published != false'
  | sort: 'date'
  | reverse
%}

<ul>
  {% for post in english_posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%Y-%m-%d' }}</time>
      {% if post.description %}
        <p>{{ post.description }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
