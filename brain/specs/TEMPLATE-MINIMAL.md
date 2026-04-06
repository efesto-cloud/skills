# [Feature] - Quick Blueprint

> **Status**: 🔵 Draft  
> **Domain**: [domain]

## What

One-sentence description.

## Entity

**Collection**: `collection_name` | **Soft Delete**: Yes/No

```
Core properties: _id, name, state, parent_id?, created_at
```

**Relationships**:
- Belongs to X
- Has many Y

**Rules**:
- Unique name
- Cannot delete if has children

---

## Operations

### Create
As an **actor**, I want to create...

**Input**: `field1`, `field2`

**Errors**: NotLoggedError, ValidationError

---

### Update
As an **actor**, I want to update...

**Input**: `id`, `field1?`

---

### Delete
As an **actor (ADMIN)**, I want to delete...

**Input**: `id`

---

### List
As an **actor**, I want to list with pagination and filters.

**Input**: `page?`, `limit?`, `filter_by?`

---

## Technical

**Indexes**:
- Primary: `_id`
- Unique: `name`

**Routes**:
```
/admin/things     → List
/admin/things/:id → Detail
/api/things       → Actions
```

**Audit**: CREATE, UPDATE, DELETE

---

## TODO

- [ ] Question 1?
- [ ] Question 2?

---

## Notes

Quick thoughts, gotchas, or decisions.
