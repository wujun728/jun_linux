---
layout: post
title: Blog With Jekyll
category: other
tags: [other]
---

## Create a blog site
For blogging, we have to specify a local folder as the root of your blog site with the commands below:  

~~~
 cd [your local folder]   
 jekyll new . 
~~~
  
As one of the results of running 'Jekyll new .', the skeleton of your blog site with a sample blog is created in the specified folder.

## Running your blog site
Theoretically Jekyll is all set and you're supposed to host your sample site with Jekyll management process right now.  
Try the command below:  

~~~
jekyll serve
~~~
  
If you are able to see similar messages as below, you are lucky:

> Configuration file: C:/**/Blog/_config.yml  
            Source: C:/**/Blog  
       Destination: C:/**/Blog/_site  
> Incremental build: disabled. Enable with --incremental  
      Generating...  
                    done in 1.413 seconds.  
  Please add the following to your Gemfile to avoid polling for changes:  
    gem 'wdm', '>= 0.1.0' if Gem.win_platform?  
> Auto-regeneration: enabled for 'C:/**/Blog'  
> Configuration file: C:/**/Blog/_config.yml  
    Server address: http://127.0.0.1:4000/  
  Server running... press ctrl-c to stop.  

it says your sample site is being served at : **http://127.0.0.1:4000/**  
Check it with your browser:    
![Sample Blog Site in Browser](/assets/images/2016/BrowsingSampleSite.PNG)  

However, I am not a lucky guy most of time :(
The 1st time I run `jekyll serve`, I got errors below:  

> C:/Ruby23/lib/ruby/2.3.0/rubygems/core_ext/kernel_require.rb:55:in `require': cannot load such file -- bundler (LoadError)  
        from C:/Ruby23/lib/ruby/2.3.0/rubygems/core_ext/kernel_require.rb:55:in `require'  
        from C:/Ruby23/lib/ruby/gems/2.3.0/gems/jekyll-3.2.1/lib/jekyll/plugin_manager.rb:34:in `require_from_bundler'  
        from C:/Ruby23/lib/ruby/gems/2.3.0/gems/jekyll-3.2.1/exe/jekyll:9:in `<top (required)>'  
        from C:/Ruby23/bin/jekyll:23:in `load'  
        from C:/Ruby23/bin/jekyll:23:in `<main>'  

*Bundler* is a gem dependency of Jekyll which is supposed to be installed with Jekyll. Apparently, it's not. After installing *Bundler* with the command bellow, I got rid of above errors:  

~~~
 gem install bundler  
~~~
   
But another dependency that is also supposed to be installed with Jekyll came out:  

> C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-.12.5/lib/bundler/resolver.rb:356:in block in verify_gemfile_dependencies_are_found!:  
> Could not find gem minima x86-mingw32 in any of the gem sources listed in your Gemfile or available on this machine.(Bundler::GemNotFound)  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/resolver.rb:331:in each  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/resolver.rb:331:in verify_gemfile_dependencies_are_found!  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/resolver.rb:200:in start  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/resolver.rb:184:in resolve  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/definition.rb:200:in resolve  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/definition.rb:140:in specs  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/definition.rb:185:in specs_for  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/definition.rb:174:in requested_specs  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/environment.rb:19:in requested_specs  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler/runtime.rb:14:in setup  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/bundler-1.12.5/lib/bundler.rb:95:in setup  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/jekyll-3.2.1/lib/jekyll/plugin_manager.rb:36:in require_from_bundler  
> from C:/Ruby23/lib/ruby/gems/2.3.0/gems/jekyll-3.2.1/exe/jekyll:9:in <top (required)>  
> from C:/Ruby23/bin/jekyll:23:in load  
> from C:/Ruby23/bin/jekyll:23:in <main>  

Finally, my blog site is able to be served successfully after I installed the dependency '**minima**'.


## else

in some case ,you must change gem source 

~~~
gem sources --add http://gems.ruby-china.org/ --remove https://rubygems.org/
~~~

congig bundle  miroor

~~~
bundle config mirror.https://rubygems.org http://gems.ruby-china.org
~~~

then  excute bundle command

now, find a nather error 

>jekyll service
>WARN: Unresolved specs during Gem::Specification.reset:
>       rouge (~> 1.7)
>       jekyll-watch (~> 1.1)
> WARN: Clearing out unresolved specs.
> Please report a bug if this causes problems.
> fatal: 'jekyll service' could not be found. You may need to install the jekyll-service gem or a related gem to be able to use this subcommand.

then  excute bundle install command

other command :

``` xml
netstat –ano|findstr “4000”

bundle exec jekyll serve
```

done!!
