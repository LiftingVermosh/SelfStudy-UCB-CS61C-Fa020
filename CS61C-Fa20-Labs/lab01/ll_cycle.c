#include <stddef.h>
#include "ll_cycle.h"

int ll_has_cycle(node *head) {
    // 快慢指针(双指针)：若链表成环，则快慢指针必然相遇 
    node *fast = head;
    node *slow = head;
    while(fast && fast->next){
        fast = fast->next->next;    // 快指针一次两步
        slow = slow->next;          // 慢指针一次一步
        if(fast == slow){
            return 1;               // 相遇则成环，返回 1
        }
    }
    return 0;
}