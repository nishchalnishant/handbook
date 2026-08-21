# LLD 04 — LRU Cache

> **Spoiler warning — this folder now contains a worked solution.**
> `CacheDemo.java` is a complete, compiling reference implementation and
> `INTERVIEW.md` is the same design spoken aloud as a 45-minute answer,
> following `notes/THE_SCRIPT.md`.
>
> **Write your own version first.** Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself — 20 minutes, no bodies — then implement, and only then
> read either file. Opening them first turns production practice back into
> reading, which is the exact gap this repo exists to close.
>
>     javac CacheDemo.java && java CacheDemo

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
