<script>
import PeopleYouMayKnowVue from '../components/PeopleYouMayKnow.vue';
import TrendsVue from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        RouterLink
    },

    // setup() {
    //     const userStore = useUserStore()

    //     return {
    //         userStore
    //     }
    // },

    data() {
        return {
            posts: [],
            users: [],
            query: '',
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .get('api/search', {
                    params: {
                        'query': this.query
                    }
                })
                .then(response => {
                    console.log('users', response.data.users);
                    console.log('posts', response.data.posts);

                    this.users = response.data.users;
                    this.posts = response.data.posts;

                })
                .catch(error => {
                    console.log(error);
                })
        }

    }
}
</script>

<template>
    <div class="max-w-7xl max-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white rounded-lg border border-gray-300 p-5">
                <form method="get" class="flex justify-between space-x-4" v-on:submit.prevent="submitForm">
                    <input v-model="query" class="rounded-lg px-5 py-3 flex-grow bg-gray-100" type="text"
                        placeholder="What are you looking for?">
                    <button type="submit" class="rounded-lg px-5 py-3 grow-0 bg-purple-400 text-white"
                        href="">Search</button>
                </form>
            </div>

            <div class="bg-white rounded-lg border border-gray-300 p-5" v-if="users.length != 0">
                <div class="grid grid-cols-4 gap-3">
                    <template v-for="user in users">
                        <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"
                            class="col-span-1 rounded-lg p-5 text-center bg-gray-100">
                            <img :src="user.get_avatar" class="mb-6 rounded-full">
                            <h2 class="font-bold text-lg">{{ user.name }}</h2>
                            <div class="flex justify-around mt-7">
                                <div class="text-gray-500 text-xs">{{ user.friends_count }} friends</div>
                                <div class="text-gray-500 text-xs">{{ user.posts_count }} posts</div>
                            </div>
                        </RouterLink>
                    </template>
                </div>
            </div>

            <div class="bg-white rounded-lg border border-gray-300 p-5 space-y-4" v-for="post in posts"
                v-bind:key="post.id">
                <PostItem v-bind:post="post" />
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnowVue />
            <TrendsVue />
        </div>
    </div>
</template>