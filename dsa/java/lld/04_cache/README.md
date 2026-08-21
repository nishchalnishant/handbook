# LLD 04 — LRU Cache (you build this)

> **Spoiler warning.** `INTERVIEW.md` in this folder is a full worked answer
> following `notes/THE_SCRIPT.md`. Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself first — 20 minutes, no bodies — and only then open it to
> compare. Opening it first turns production practice back into reading.

## Requirements
    class Cache<K, V>
        V get(K key)              // null if absent
        void put(K key, V value)  // evict when over capacity
        int size()

Eviction policy is an interface with at least: LRU, LFU, FIFO.

## The interesting constraint
Get and put must both be O(1). That means HashMap + doubly linked list —
the map finds the node, the list tracks recency. Draw the pointers on
paper before coding; this is the one problem here where drawing first helps.

Java gives you LinkedHashMap with an access-order flag that does this for
free. Implement it BY HAND first, then look at LinkedHashMap and compare.
The hand-built version is what an interviewer wants to see.

## Done when
- 200 random operations agree with a naive reference implementation
- capacity is never exceeded
- you can explain out loud why a singly linked list is not enough

## Stretch
- add TTL expiry per entry
- add a listener fired on eviction (that's the observer pattern)
