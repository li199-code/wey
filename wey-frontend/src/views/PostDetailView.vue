<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center col-span-2">
            <div class="p-4 bg-white border border-gray-200 rounded-lg mb-4" v-if="post.id">
                <PostItem v-bind:post="post" />
            </div>

            <div class="p-4 ml-6 bg-white border border-gray-200 rounded-lg" v-for="comment in post.comments"
                v-bind:key="comment.id">
                <CommentItem v-bind:comment="comment" />
            </div>

            <div class="bg-white rounded-lg">
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
import CommentItem from '../components/CommentItem.vue'
import axios from 'axios';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        CommentItem,
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`api/post/${this.$route.params.id}/`)
                .then(response => {
                    console.log('post', response.data);
                    this.post = response.data;
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
