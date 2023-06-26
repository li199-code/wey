<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg">
                <PostForm v-bind:user="null" v-bind:posts="posts" />
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <PostItem v-bind:post="post" v-on:handleDelete="handleDelete" />
            </div>

            <Paginator :has_previous="has_previous" :has_next="has_next" :total_pages="total_pages" 
                :current_page="current_page"  @getFeed="getFeed" />



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
import PostForm from '../components/PostForm.vue'
import Paginator from '../components/Paginator.vue';
import axios from 'axios';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        PostForm,
        Paginator,
    },

    data() {
        return {
            posts: [],
            has_previous: false,
            has_next: false,
            total_pages: 0,
            current_page: 0,
            body: '',
            url: null,
            is_private: false,
        }
    },

    mounted() {
        this.getFeed(1)
    },

    methods: {
        getFeed(page) {
            axios
                .get(`api/post/?page=${page}`)
                .then(response => {
                    console.log('data', response);
                    this.posts = response.data.posts;
                    this.has_previous = response.data.has_previous;
                    this.has_next = response.data.has_next;
                    this.total_pages = response.data.total_pages;
                    this.current_page = response.data.current_page;                   
                    
                })
                .catch(error => {
                    console.log('error', error);
                })
        },

        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        handleDelete(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        }

    }
}

</script>