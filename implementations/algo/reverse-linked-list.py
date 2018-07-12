def reverse_link_list(head):
    if not head:
        return head

    if not head.next:
        return head

    dummy = LinkListNode(-1)

    dummy.next = head

    has_reversed = dummy
    to_be_reversed = head

    while to_be_reversed:
        curr = to_be_reversed
        to_be_reversed = to_be_reversed.next
        curr.next = has_reversed
        has_reversed = curr

    head.next = None

    return has_reversed
