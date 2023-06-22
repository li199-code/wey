<template>
    <div class="flex justify-between items-center mb-6">
        <RouterLink :to="{ name: 'profile', params: { 'id': post.created_by.id } }"
            class="flex items-center justify-between space-x-5">
            <img class="w-[40px] rounded-full" :src="post.created_by.get_avatar" alt="">
            <p class="font-bold text-lg">{{ post.created_by.name }}</p>
        </RouterLink>
        <p class="text-lg text-gray-400">{{ post.created_at_formatted }} ago</p>
    </div>

    <template v-if="post.attachments.length">
        <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
    </template>

    <p>{{ post.body }}</p>
    <div class="flex justify-between items-center mt-5">
        <div class="flex items-center justify-between space-x-5">
            <div class="flex items-center justify-between space-x-2">
                <button @click="handleLike(post.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                    </svg>
                </button>
                <span class="text-gray-400 text-xs">{{ post.likes_count }} likes</span>
            </div>
            <div class="flex items-center justify-between space-x-2">
                <RouterLink :to="{ name: 'postdetail', params: { 'id': post.id } }">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443 48.282 48.282 0 005.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
                    </svg>
                </RouterLink>
                <span class="text-gray-400 text-xs">{{ post.comments_count }} comments</span>
            </div>
            <div class="flex items-center justify-between space-x-2" v-if="post.is_private">
                <span class="text-gray-600 text-xs">Private</span>
            </div>
        </div>
        <div @click="handleToggle">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
            </svg>
        </div>
    </div>
    <div class="flex items-center space-x-5 mt-5 text-sm" v-if="toggle">
        <div class="flex items-center justify-between space-x-2 text-red-500" v-if="userStore.user.id == post.created_by.id"
            @click="handleDelete">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
            </svg>

            <span>Delete</span>
        </div>
        <div class="flex items-center justify-between space-x-2 text-orange-300"
            v-if="userStore.user.id !== post.created_by.id" @click="showReportModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
            </svg>

            <span>Report</span>
        </div>
    </div>

    <div v-if="showModal">
        <form class="space-x-2" v-on:submit.prevent="submitReport" method="post">
            <textarea v-model="reportReason" class="p-4 w-full bg-gray-100 rounded-lg"
                placeholder="Report reason"></textarea>

            <button class="inline-block py-2 px-3 bg-purple-600 text-white rounded-lg">Submit</button>
            <button @click="hideReportModal"
                class="inline-block py-2 px-3 bg-gray-600 text-white rounded-lg">Dismiss</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';

export default {
    setup() {
        const ToastStore = useToastStore()
        const userStore = useUserStore()

        return {
            ToastStore,
            userStore,
        }
    },

    props: {
        post: Object,
    },

    emits: ['handleDelete'],

    data() {
        return {
            toggle: false,
            showModal: false,
            reportReason: ''
        }
    },

    methods: {
        handleToggle() {
            this.toggle = !this.toggle;
        },

        handleLike(postid) {
            axios
                .post(`/api/post/like/${postid}/`)
                .then(response => {
                    if (response.data.message === 'like created successfully') {
                        this.post.likes_count += 1
                    } else {
                        this.ToastStore.showToast(5000, 'You already like it!', 'bg-red-500 text-white')
                    }
                })
                .catch(err => {
                    console.log(err);
                })
        },

        handleDelete() {
            this.$emit('handleDelete', this.post.id)
            alert('Are you sure to delete?');
            axios
                .delete(`api/post/${this.post.id}/`)
                .then(response => {
                    if (response.status = 204) {
                        this.ToastStore.showToast(5000, 'Post deleted!', 'bg-green-500 text-white')
                    }
                    else {
                        this.ToastStore.showToast(5000, 'Something went wrong!', 'bg-red-500 text-white')
                    }
                })
                .catch(err => {
                    console.log(err);
                })
        },

        showReportModal() {
            this.showModal = true;
        },
        hideReportModal() {
            this.showModal = false;
        },
        submitReport() {
            // console.log('提交举报，举报理由：', this.reportReason);

            let formData = new FormData();
            formData.append('reason', this.reportReason)

            axios
                .post(`api/post/${this.post.id}/report/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    // console.log(response.data);
                    this.ToastStore.showToast(5000, 'Post Reported!', 'bg-green-500 text-white')
                })
                .catch(err => {
                    this.ToastStore.showToast(5000, 'Something went wrong!', 'bg-red-500 text-white')
                })


            this.hideReportModal();
        }
    }
}
</script>