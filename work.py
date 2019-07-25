import link_crawling

movie_list = link_crawling.read_movie_list_test()
site_list = link_crawling.read_site_list()
link_crawling.body(site_list, movie_list)
