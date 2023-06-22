<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left">
            <div class="bg-white rounded-lg p-5 text-center">
                <img :src="user.get_avatar" class="mb-6 rounded-full">
                <h2 class="font-bold text-lg">{{ user.name }}</h2>
                <div class="flex justify-around mt-7">
                    <div class="text-gray-500 text-xs">{{ user.friends_count }} friends</div>
                    <div class="text-gray-500 text-xs">{{ user.posts_count }} posts</div>
                </div>
            </div>
        </div>
        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg border border-gray-300 p-5 space-y-4">
                <h2 class="font-bold text-lg text-center">Friends Requests List</h2>
                <hr>
                <div v-for="item in friendshiprequest" v-bind:key="item.id">
                    <div class="flex justify-between items-center">
                        <div class="flex items-center justify-between space-x-2">
                            <img class="w-[40px] rounded-full" :src="item.created_by.get_avatar" alt="">
                            <RouterLink :to="{ name: 'profile', params: { 'id': item.created_by.id } }" class="font-bold">{{
                                item.created_by.name }}</RouterLink>
                        </div>
                        <div class="space-x-5 flex align-middle">
                            <button :disabled="ishandled" @click="handleRequest(item.id, 'accepted')"
                                class="bg-green-700 text-white rounded-lg px-3 py-2"
                                :class="{ 'opacity-50 cursor-not-allowed': ishandled }">Accept</button>
                            <button :disabled="ishandled" @click="handleRequest(item.id, 'rejected')"
                                class="bg-red-700 text-white rounded-lg px-3 py-2"
                                :class="{ 'opacity-50 cursor-not-allowed': ishandled }">Reject</button>
                        </div>
                    </div>
                </div>

            </div>

            <div class="bg-white rounded-lg border border-gray-300 p-5 space-y-4">
                <h2 class="font-bold text-lg text-center">Friends List</h2>
                <hr>
                <div class="flex justify-between items-center" v-for=" friend in friends" v-bind:key="friend.id">
                    <div class=" flex items-center justify-between space-x-2">
                        <img class="w-[40px] rounded-full" :src="friend.get_avatar" alt="">
                        <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }" class="font-bold">{{ friend.name
                        }}
                        </RouterLink>
                    </div>
                    <div class="space-x-5 flex align-middle">
                        <div class="text-gray-500 text-sm">{{ friend.friends_count }} friends</div>
                        <div class="text-gray-500 text-sm">{{ friend.posts_count }} posts</div>
                    </div>
                </div>

            </div>

        </div>
        <div class="main-right space-y-4">
            <PeopleYouMayKnowVue />
            <TrendsVue />
        </div>
    </div>
</template>

<script>
import PeopleYouMayKnowVue from '../components/PeopleYouMayKnow.vue';
import TrendsVue from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
    },

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    mounted() {
        this.getFriends();
    },

    data() {
        return {
            user: {},
            friendshiprequest: [],
            friends: [],
            ishandled: false,
        }
    },

    methods: {
        getFriends() {
            axios
                .get(`/api/friend/${this.$route.params.id}/`)
                .then(response => {
                    console.log('friends', response.data.friends)
                    console.log('friendshiprequest', response.data.friendshiprequest)
                    this.friends = response.data.friends
                    this.friendshiprequest = response.data.friendshiprequest
                    this.user = response.data.user
                    console.log('this.user', this.user)
                })
                .catch(error => {
                    console.log(error)
                })
        },

        handleRequest(pk, status) {
            console.log('pk', pk);
            console.log('status', status);
            axios
                .post(`/api/friend/${this.$route.params.id}/`, {
                    'pk': pk,
                    'status': status
                })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error)
                });
            this.ishandled = true
        }





    }
}

</script>

