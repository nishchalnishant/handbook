# LLD problem bank — 44 problems

Specs and blank `ATTEMPT.md` skeletons for every problem in the SystemDesign
repo, all driven by the same procedure: **`../../notes/THE_SCRIPT.md`**.

**There are no answers here on purpose.** Each folder links to its worked solution
in the source repo. Attempt first, compare second. The five problems already worked
end to end live one level up in `lld/` and have `INTERVIEW.md` files instead.

## How to work through this

1. Pick a problem. Start with the Core five, then Easy/Medium.
2. Fill in `ATTEMPT.md`. Phases 1–4 only on your first pass — 20 minutes, no bodies.
3. Write the Java in the folder and run it.
4. Open the answer key. Log the delta in `../../notes/error_log.md`.

Round 1 of the practice plan is Phases 1–4 only. You can do four of those in the
time one full attempt takes, and they are 80% of the grade.

## Progress

Tick when the ATTEMPT is filled in **and** the code runs.

### Core — do these first

| ? | # | Problem | Diff | Patterns | Folder |
|---|---|---|---|---|---|
| ✅ | 01 | Design a Parking Lot | Medium | Singleton (ParkingLot), Strategy (pricing), Factory (spot assignment), Template Method | [`01_parking_lot/`](../01_parking_lot/) — **worked** |
| ✅ | 02 | Design a Rate Limiter | Medium | Strategy (algorithm), per-user bucket isolation, lazy refill | [`03_rate_limiter/`](../03_rate_limiter/) — **worked** |
| [ ] | 03 | Design Tic-Tac-Toe | Easy | Strategy (win checker), State enum, counter-based O(1) win detection | [`p03_tic_tac_toe/`](p03_tic_tac_toe/) |
| [ ] | 04 | Design a Vending Machine | Medium | State pattern (machine states), Strategy (payment), Command (dispense) | [`p04_vending_machine/`](p04_vending_machine/) |
| ✅ | 05 | Design Splitwise | Medium | Strategy (split type), Graph (debt simplification), net balance tracking | [`05_splitwise/`](../05_splitwise/) — **worked** |

### Frequently asked

| ? | # | Problem | Diff | Patterns | Folder |
|---|---|---|---|---|---|
| [ ] | 06 | Design BookMyShow | Hard | State (booking status), Strategy (payment), TTL-based seat locking, Template Method (booking flow) | [`p06_bookmyshow/`](p06_bookmyshow/) |
| [ ] | 07 | Design Chess | Hard | Polymorphism (piece hierarchy), State enum, Template Method | [`p07_chess/`](p07_chess/) |
| [ ] | 08 | Design Snake and Ladder | Easy | Strategy (dice), Observer (position events), Factory (board setup) | [`p08_snake_and_ladder/`](p08_snake_and_ladder/) |
| ✅ | 09 | Design Elevator System | Hard | State (elevator state), Strategy (scheduling), Observer (floor requests) | [`02_elevator/`](../02_elevator/) — **worked** |
| [ ] | 10 | Design a Nested Comment System | Medium | Composite (tree of comments), Strategy (sort), Observer (notifications) | [`p10_nested_comment_system/`](p10_nested_comment_system/) |
| [ ] | 11 | Design a Hotel Management System | Medium | Factory (room types), State (room/reservation status), Strategy (pricing) | [`p11_hotel_management_system/`](p11_hotel_management_system/) |
| [ ] | 12 | Design an ATM System | Medium | State (ATM states), Strategy (cash dispensing), Template Method (transaction flow) | [`p12_atm_system/`](p12_atm_system/) |
| ✅ | 13 | Design an LRU Cache | Medium | Custom data structure (DoublyLinkedList + HashMap) | [`04_cache/`](../04_cache/) — **worked** |
| [ ] | 14 | Design a Food Delivery System | Medium | State (order lifecycle), Observer (tracking), Strategy (delivery assignment) | [`p14_food_delivery_system/`](p14_food_delivery_system/) |
| [ ] | 15 | Design Locker Service | Medium | Strategy (size matching), Inheritance (locker sizes), Factory | [`p15_locker_service/`](p15_locker_service/) |
| [ ] | 16 | Design Notification System | Medium | Observer, Strategy (channel), Chain of Responsibility (retry/fallback) | [`p16_notification_system/`](p16_notification_system/) |
| [ ] | 17 | Design Coupon System | Medium | Composite (coupon stacking), Chain of Responsibility (validation), Strategy (discount type) | [`p17_coupon_system/`](p17_coupon_system/) |

### Domain-specific

| ? | # | Problem | Diff | Patterns | Folder |
|---|---|---|---|---|---|
| [ ] | 18 | Design Mentorship Platform | Medium | Strategy (matching), Observer (booking events), Conflict detection (interval overlap) | [`p18_mentorship_platform/`](p18_mentorship_platform/) |
| [ ] | 19 | Design a Logger Library | Medium | Chain of Responsibility (log level filtering), Strategy (sink/appender), Singleton (logger instance) | [`p19_logger_library/`](p19_logger_library/) |
| [ ] | 20 | Design a Library Management System | Medium | State (book copy status), Strategy (fine calculation), Observer (reservation notifications) | [`p20_library_management_system/`](p20_library_management_system/) |
| [ ] | 21 | Design an Order Management System | Medium | State (order status), Saga (multi-step order flow), Observer (status notifications) | [`p21_order_management_system/`](p21_order_management_system/) |
| [ ] | 22 | Design a Ride Sharing System | Hard | State (ride status), Strategy (matching/fare), Observer (driver location updates) | [`p22_ride_sharing_system/`](p22_ride_sharing_system/) |
| [ ] | 23 | Design a Pub-Sub Messaging System | Hard | Observer, Strategy (delivery guarantee), Command (message processing) | [`p23_pub_sub_messaging_system/`](p23_pub_sub_messaging_system/) |
| [ ] | 24 | Design Inventory Management System | Medium | Observer (stock alerts), Strategy (reservation), Optimistic locking (concurrent updates) | [`p24_inventory_management_system/`](p24_inventory_management_system/) |

### Advanced / niche

| ? | # | Problem | Diff | Patterns | Folder |
|---|---|---|---|---|---|
| [ ] | 25 | Design Minesweeper | Medium | Flood Fill (BFS/DFS), State Machine (cell state), Factory (board setup) | [`p25_minesweeper/`](p25_minesweeper/) |
| [ ] | 26 | Design S3 Object Storage / File System | Hard | Composite (folder hierarchy), Metadata separation, Strategy (permissions) | [`p26_s3_object_storage_file_system/`](p26_s3_object_storage_file_system/) |
| [ ] | 27 | Design Search Engine (Inverted Index) | Hard | Inverted Index, TF-IDF ranking, Strategy (tokenizer), Iterator (result pagination) | [`p27_search_engine/`](p27_search_engine/) |
| [ ] | 28 | Design Tetris | Hard | Factory (tetromino types), Strategy (rotation), Command (move/rotate/drop) | [`p28_tetris/`](p28_tetris/) |
| [ ] | 29 | Design Version Control System | Hard | Command (commit/checkout), Graph (DAG of commits), Composite (directory tree) | [`p29_version_control_system/`](p29_version_control_system/) |
| [ ] | 30 | Design HTTP Tunneling Service | Hard | Proxy, Observer, Strategy (protocol handling) | [`p30_http_tunneling_service/`](p30_http_tunneling_service/) |
| [ ] | 31 | Design Text Editor | Hard | Command Pattern (undo/redo), Gap Buffer (efficient insert/delete at cursor) | [`p31_text_editor/`](p31_text_editor/) |
| [ ] | 32 | Design Download Manager | Hard | Thread pool (parallel chunks), State Machine (download lifecycle), Strategy (retry) | [`p32_download_manager/`](p32_download_manager/) |
| [ ] | 33 | Design Unlock Pattern | Medium | DFS / Backtracking, Adjacency constraint validation, Graph traversal | [`p33_unlock_pattern/`](p33_unlock_pattern/) |
| [ ] | 34 | Design Lock-Free Queue | Hard | Compare-and-Swap (CAS), ABA problem, Michael-Scott queue algorithm | [`p34_lock_free_queue/`](p34_lock_free_queue/) |
| [ ] | 35 | Design Concurrent LRU Cache | Hard | LRU eviction (DoublyLinkedList + HashMap), Striped locking (segment-level), Thread safety | [`p35_concurrent_lru_cache/`](p35_concurrent_lru_cache/) |
| [ ] | 36 | Design High-Contention Counter | Hard | Striped counters (LongAdder pattern), CAS loops, Eventual consistency | [`p36_high_contention_counter/`](p36_high_contention_counter/) |

### Additional

| ? | # | Problem | Diff | Patterns | Folder |
|---|---|---|---|---|---|
| [ ] | 37 | Design Stack Overflow | Medium | Strategy (ranking), Observer (answer/comment notifications), State-ish (vote transitions), Composite (Question → Answer → Comment) | [`p37_stack_overflow/`](p37_stack_overflow/) |
| [ ] | 38 | Design a Social Network (LinkedIn / Facebook) | Hard | Observer (feed/notification fan-out), Strategy (feed ranking), State (connection lifecycle) | [`p38_social_network/`](p38_social_network/) |
| [ ] | 39 | Design a Stock Brokerage System | Hard | Strategy (order execution), Observer (price-triggered limit orders), Command (order lifecycle) | [`p39_stock_brokerage_system/`](p39_stock_brokerage_system/) |
| [ ] | 40 | Design a Digital Wallet Service | Hard | Double-Entry Ledger, Idempotency Key + Dedupe Table, Lock Ordering (deadlock avoidance), Command (TransferRequest) | [`p40_digital_wallet_service/`](p40_digital_wallet_service/) |
| [ ] | 41 | Design a Car Rental System | Medium | Strategy (pricing), Factory (vehicle creation), interval-overlap scheduling | [`p41_car_rental_system/`](p41_car_rental_system/) |
| [ ] | 42 | Design a Restaurant Management System | Medium | State (order-item lifecycle), Observer (kitchen display notifications), Strategy (bill splitting) | [`p42_restaurant_management_system/`](p42_restaurant_management_system/) |
| [ ] | 43 | Design an Airline Management System | Medium | State (Seat lifecycle), Strategy (fare pricing), Factory (seat map construction), Observer (waitlist notification) | [`p43_airline_management_system/`](p43_airline_management_system/) |
| [ ] | 44 | Design a Task Management System | Medium | Observer (activity log/notifications), Command (undo/redo task moves), State (status transitions) | [`p44_task_management_system/`](p44_task_management_system/) |

## Counts

- 44 problems total — **5 worked** (`lld/01`–`05`), **39 to attempt**
- Easy 2 · Medium 24 · Hard 18

## A note on the source's pseudocode

The answer keys write their *class design* sections in Python-flavoured pseudocode
(`Dict[int, int]`, `Optional[Card]`, `snake_case`, `-> None`) even though the
implementations are real Java. Translate as you read — that mapping is itself the
skill being built here:

| Source pseudocode | Java |
|---|---|
| `Dict[int, int]` | `Map<Integer, Integer>` |
| `List[Order]` | `List<Order>` |
| `Optional[Card]` | `Optional<Card>` or a nullable field |
| `Set[str]` | `Set<String>` |
| `can_dispense(amount) -> bool` | `boolean canDispense(long amount)` |
| `- balance: float` | `private long balanceInMinorUnits;` (money is never a float) |
| `+ get_balance() -> float` | `long balance()` |

Write Java in your `ATTEMPT.md`, never the pseudocode. Reading Python-shaped
designs is the wrong reinforcement for the gap you are closing.
