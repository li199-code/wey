<template>
    <div class="flex justify-between items-center mb-2">
        <RouterLink :to="{ name: 'profile', params: { 'id': comment.created_by.id } }"
            class="flex items-center justify-between space-x-5">
            <img class="w-[40px] rounded-full" :src="comment.created_by.get_avatar" alt="">
            <p class="font-bold text-lg">{{ comment.created_by.name }}</p>
        </RouterLink>
        <p class="text-lg text-gray-400">{{ comment.created_at_formatted }} ago</p>
    </div>
    <!-- <img class="rounded-lg w-full"
                    src="https://images.unsplash.com/photo-1661956602868-6ae368943878?ixlib=rb-4.0.3&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2670&q=80"
                    alt=""> -->
    <p>{{ comment.body }}</p>
</template>


<script>
import { RouterLink } from 'vue-router'

export default {
    props: {
        comment: Object,
    },
    components: { RouterLink }
}
</script>
