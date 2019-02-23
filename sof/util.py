def remove_duplicate_item(items:list, key):
    seen = set()
    distinct_items = []
    for item in items:
        if key(item) not in seen:
            seen.add(key(item))
            distinct_items.append(item)
    return distinct_items



