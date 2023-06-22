<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg">
                <PostForm v-bind:user="null" v-bind:posts="posts" />
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <PostItem v-bind:post="post" v-on:handleDelete="handleDelete" />
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
import PostForm from '../components/PostForm.vue'
import axios from 'axios';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        PostForm,
    },

    data() {
        return {
            posts: [],
            body: '',
            url: null,
            is_private: false,
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('api/post')
                .then(response => {
                    console.log('data', response.data);
                    this.posts = response.data
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