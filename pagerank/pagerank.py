import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_probs = {}
    if len(corpus[page]) == 0:
        for cur_page in corpus:
            page_probs[cur_page] = 1.0/len(corpus) 
    else:
        for cur_page in corpus:
            prob = 0
            if cur_page in corpus[page]:
                prob = damping_factor/len(corpus[page])
            page_probs[cur_page] = prob + (1-damping_factor)/len(corpus) 
    return page_probs 


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_probs = {page:0.0 for page in corpus}
    page = random.choice(list(corpus))
    page_probs[page] = 1
    for i in range(n-1):
        next_page_probs = transition_model(corpus,page,damping_factor)
        prob = random.uniform(0,1)
        probs_sum = 0.0
        for next_page in next_page_probs:
            probs_sum += next_page_probs[next_page]
            if probs_sum >= prob:
                page = next_page
                break
        page_probs[page] += 1 
    
    for pg in page_probs: page_probs[pg] /= n
    return page_probs
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_len = len(corpus)
    page_probs = {page:(1.0/corpus_len) for page in corpus}

    while True:
        page_probs_past = page_probs.copy()
        for page in page_probs_past:
            links_probs = 0.0
            for pg in page_probs_past:
                if page in corpus[pg]:
                    links_probs += page_probs_past[pg] / len(corpus[pg])
                elif len(corpus[pg]) == 0:
                    links_probs += page_probs_past[pg] / corpus_len
            links_probs *= damping_factor
            page_probs[page] = (1 - damping_factor)/corpus_len + links_probs
        target_accuaracy = True
        for page in page_probs:
            if abs(page_probs[page] - page_probs_past[page]) > 0.001:
                target_accuaracy = False
                break
        if target_accuaracy:
            break
    return page_probs


if __name__ == "__main__":
    main()
