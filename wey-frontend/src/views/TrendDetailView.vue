<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg p-4 font-bold text-lg">#{{ $route.params.hashtag }}</div>

            <div class="bg-white rounded-lg">
                <PostForm v-bind:user="null" v-bind:posts="posts" />

            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <PostItem v-bind:post="post" />
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
import PostForm from '../components/PostForm.vue';
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
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        '$route.params.hashtag': {
            handler: function () {
                this.getFeed();
                this.body = '#' + this.$route.params.hashtag;
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        getFeed() {
            axios
                .get('api/search', {
                    params: {
                        'query': this.$route.params.hashtag
                    }
                })
                .then(response => {
                    console.log('data', response.data.posts);
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error', error);
                })
        },

        submitForm() {
            axios
                .post('api/post/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('response', response.data);
                    this.body = ''
                    this.posts.unshift(response.data)
                })
                .catch(error => {
                    console.log(error);
                })
        }

    }
}

</script>