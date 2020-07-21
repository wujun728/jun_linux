---
layout: page
title: MongoDB 系列文章
titlebar: MongoDB
subtitle: <span class="mega-octicon octicon-clippy"></span>&nbsp;&nbsp; MongoDB 系列教程
menu: mongodb
css: ['blog-page.css']
permalink: /mongodb
keywords: MongoDB,MongoDB 集群,部署,搭建,MongoDB 教程
---

<div class="row">

    <div class="col-md-12">

        <ul id="posts-list">
            {% for post in site.posts %}
                {% if post.category=='mongodb'  or post.keywords contains 'mongodb' %}
                <li class="posts-list-item">
                    <div class="posts-content">
                        <span class="posts-list-meta">{{ post.date | date: "%Y-%m-%d" }}</span>
                        <a class="posts-list-name bubble-float-left" href="{{ site.url }}{{ post.url }}">{{ post.title }}</a>
                        <span class='circle'></span>
                    </div>
                </li>
                {% endif %}
            {% endfor %}
        </ul> 

        <!-- Pagination -->
        {% include pagination.html %}

        <!-- Comments -->
       <div class="comment">
         {% include comments.html %}
       </div>
    </div>

</div>
<script>
    $(document).ready(function(){

        // Enable bootstrap tooltip
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });

    });
</script>