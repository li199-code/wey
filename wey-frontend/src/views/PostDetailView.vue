<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center col-span-2">
            <div class="p-4 bg-white border border-gray-200 rounded-lg mb-4" v-if="post.id">
                <PostItem v-bind:post="post" />
            </div>

            <div class="p-4 ml-6 bg-white border border-gray-200 rounded-lg" v-for="comment in comments_paginator.comments"
                v-bind:key="comment.id">
                <CommentItem v-bind:comment="comment" />
            </div>

            <Paginator :has_previous="comments_paginator.has_previous" :has_next="comments_paginator.has_next" :total_pages="comments_paginator.total_pages" 
                :current_page="comments_paginator.current_page"  @getFeed="getPost" />           

            <div class="bg-white rounded-lg mt-4">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Say something..."></textarea>
                    </div>
                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button type="submit"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>

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
import Paginator from '../components/Paginator.vue';
import CommentItem from '../components/CommentItem.vue'
import axios from 'axios';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        CommentItem,
        Paginator,
    },

    data() {
        return {
            post: {
                id: null,
            },
            comments_paginator: {
                comments: [],
                has_previous: false,
                has_next: false,
                total_pages: 0,
                current_page: 0,
            },

            body: ''
        }
    },

    mounted() {
        this.getPost(1)
    },

    methods: {
        getPost(comment_page) {
            axios
                .get(`api/post/${this.$route.params.id}/?comment_page=${comment_page}`)
                .then(response => {
                    console.log('post', response.data);
                    this.post = response.data.post;
                    this.comments_paginator = response.data.comments_paginator;
                })
                .catch(error => {
                    console.log('error', error);
                })
        },

        submitForm() {
            axios
                .post(`api/post/comment/${this.$route.params.id}/`, {
                    'body': this.body,
                })
                .then(response => {
                    console.log('data', response.data)

                    this.post.comments.push(response.data.comment)
                    console.log('this.post.comments', this.post.comments)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log(error);
                })
        }

    }
}

</script>
