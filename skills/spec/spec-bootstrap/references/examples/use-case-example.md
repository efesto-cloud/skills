---
use-case: IssueInvoiceUseCase
status: stable
module: billing
entity: Invoice
---

# Use Case: IssueInvoiceUseCase

## Intent
Allow a billing manager to transition a draft invoice to issued status, locking its line items and recording the issuance timestamp.

## Dependencies (injected via Inversify)

| Token                           | Interface                  | Used for                                |
|---------------------------------|----------------------------|-----------------------------------------|
| `BILLING_INVOICE_REPOSITORY`    | `IInvoiceRepository`       | Loading and persisting the invoice      |
| `BILLING_CUSTOMER_REPOSITORY`   | `ICustomerRepository`      | Verifying the customer still exists     |

## Input

**DTO:** `IssueInvoiceInputDto`

| Field      | Type        | Required | Rules                                      |
|------------|-------------|----------|--------------------------------------------|
| invoiceId  | string      | yes      | Non-empty UUID                             |
| issuedAt   | Date        | no       | Defaults to `new Date()` if not provided   |

## Output

**DTO:** `InvoiceDto`

All fields are always present. `issuedAt` will be set to the value used during issuance.

## Steps

1. Validate `invoiceId` is a non-empty string — throw `InvoiceIdRequiredError` if not
2. Load `Invoice` by `invoiceId` via `IInvoiceRepository.findById()` — throw `InvoiceNotFoundError` if null
3. Verify `Invoice.status` is `draft` — throw `InvalidInvoiceStatusError` if not
4. Load `Customer` by `invoice.customerId` via `ICustomerRepository.findById()` — throw `CustomerNotFoundError` if null
5. Call `invoice.issue(issuedAt ?? new Date())` — entity method sets `status = issued`, `issuedAt`, and freezes `lineItems`
6. Persist via `IInvoiceRepository.save(invoice)`
7. Return mapped `InvoiceDto`

**Note on ordering:** all validation and I/O reads before any mutation; persist last.

## Errors

| Error                         | Condition                                              |
|-------------------------------|--------------------------------------------------------|
| `InvoiceIdRequiredError`      | `invoiceId` is empty or missing                        |
| `InvoiceNotFoundError`        | No invoice found for the given `invoiceId`             |
| `InvalidInvoiceStatusError`   | Invoice is not in `draft` status                       |
| `CustomerNotFoundError`       | Customer referenced by the invoice no longer exists    |

## Acceptance criteria

- WHEN `invoiceId` is missing THEN throw `InvoiceIdRequiredError` before any I/O
- WHEN invoice does not exist THEN throw `InvoiceNotFoundError`
- WHEN invoice status is `issued`, `paid`, or `cancelled` THEN throw `InvalidInvoiceStatusError`
- WHEN customer no longer exists THEN throw `CustomerNotFoundError`
- WHEN all preconditions are met THEN return `InvoiceDto` with `status = issued` and `issuedAt` set

## Does NOT

- Does not send the invoice PDF or email to the customer (that is an application service concern)
- Does not charge the customer or interact with Stripe (payment is a separate use case)
- Does not validate the customer's credit limit or account standing
- Does not generate the `invoiceNumber` (assumed already set during `CreateInvoiceUseCase`)
- Does not call other use cases directly

## Repository interface hints

- `IInvoiceRepository.findById(id: string): Promise<Invoice | null>`
- `IInvoiceRepository.save(invoice: Invoice): Promise<void>`
- `ICustomerRepository.findById(id: string): Promise<Customer | null>`

## Open questions / assumptions ⚠️
- ⚠️ Assumed `issuedAt` defaults to server time if not provided — confirm whether the caller must always supply it
- ⚠️ Assumed customer existence check is required at issuance — verify if this check can be skipped for performance
