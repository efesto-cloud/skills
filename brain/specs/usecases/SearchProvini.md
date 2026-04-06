# SearchProvini

> **Status**: ⚪ Implemented  
> **Domain**: Provino  
> **Actor**: Operator

Search provini by name, surname, or cemetery with filters.

---

## Description

As an **operator**, I want to search provini using a single text query that matches across name, surname, and cemetery. I can also filter by impresa, creation date range, and cemetery. Results are paginated and sorted by relevance.

---

## Input

```typescript
{
  q?: string,                    // Search text (fuzzy match on nome/cognome/cimitero)
  impresa_id?: string,           // Filter by impresa
  cimitero?: string,             // Filter by cemetery (exact match)
  created_from?: string,         // Filter by creation date (ISO date string)
  created_to?: string,           // Filter by creation date
  include_deleted?: boolean,     // Include soft-deleted provini (default: false)
  page?: number,                 // Page number (default: 1)
  limit?: number,                // Items per page (default: 20)
}
```

All filters are optional. If `q` is empty, returns all provini (with other filters applied).

---

## Returns

```typescript
Page<IProvino>  // Paginated results with total count
```

**Page structure**:
```typescript
{
  items: IProvino[],
  total: number,
  page: number,
  limit: number,
  totalPages: number
}
```

---

## Business Logic

1. Validate operator session
2. Build query:
   - If `q` provided, use text search on nome/cognome/cimitero (case-insensitive, partial match)
   - Apply `impresa_id` filter if provided
   - Apply `cimitero` filter if provided (exact match)
   - Apply date range filters if provided
   - By default, exclude `deleted_at != null` unless `include_deleted=true`
3. Sort by relevance (text score) when `q` is used, otherwise by `created_at DESC`
4. Apply pagination
5. Return page of provini

---

## Special Cases

- **Empty query**: If `q` is empty or not provided, returns all provini (with filters)
- **Case-insensitive**: "mar" matches "Mario", "maria", "Mariano"
- **Partial words**: "ro" matches "Rossi", "Roberto"
- **Multiple fields**: Search matches nome OR cognome OR cimitero
- **Cemetery filter**: Exact match (not fuzzy) - useful for filtering after search
- **Deleted items**: Excluded by default, operators can include them with flag

---

## Errors

- **NotLoggedError** - Invalid/expired operator session

No other errors expected (empty results are success, not error).

---

## Performance Notes

- Text index on `{ nome: "text", cognome: "text", cimitero: "text" }` for fuzzy search
- Compound index `{ impresa_id: 1, deleted_at: 1, created_at: -1 }` for filtered lists
- For large datasets (10k+ provini), search may take 100-500ms
- Consider adding dedicated search service (Elasticsearch) if becomes bottleneck

---

## Related Entities

- [Provino](../entities/Provino.md) - Main entity
- [ImpresaFunebre](../entities/ImpresaFunebre.md) - Referenced via `impresa_id`

---

## Related Use Cases

- [CreateProvino](./CreateProvino.md) - Create new provino
- [GetProvino](./GetProvino.md) - Get single provino
- [ListProvini](./ListProvini.md) - Simple paginated list (no search)

---

## Implementation

**Use Case**: `/src/useCase/provino/impl/SearchProvini.ts`  
**Interface**: `/src/useCase/provino/ISearchProvini.ts`  
**Repository Method**: `IProvinoRepo.search(ctx, filters, pagination)`  
**DI Symbol**: `Symbols.UseCase.Provino.Search`

**Audit**: Not audited (read-only operation)

---

## Admin Route

**Loader**: `/packages/admin-webapp/app/routes/admin.provini._index.tsx`

```typescript
export async function loader({ request }: Route.LoaderArgs) {
  const url = new URL(request.url);
  const params = {
    q: url.searchParams.get("q") ?? undefined,
    impresa_id: url.searchParams.get("impresa_id") ?? undefined,
    cimitero: url.searchParams.get("cimitero") ?? undefined,
    // ... other params
  };
  
  const useCase = container.get<ISearchProvini>(Symbols.UseCase.Provino.Search);
  const result = await useCase.execute({ operator_session_id, ...params });
  
  return result; // Page<IProvino>
}
```

---

## Client Route

Also exposed in client webapp:

**Route**: `/provini` (impresa can search their own provini)

**Loader**: Similar but filtered by session's `impresa_id` automatically

---

## Future Enhancements

- [ ] Save search filters as presets
- [ ] Recent searches dropdown
- [ ] Advanced filters (date of death year only, month+year, etc.)
- [ ] Export search results as CSV

See [../drafts/feature-requests.md](../drafts/feature-requests.md) for details.
