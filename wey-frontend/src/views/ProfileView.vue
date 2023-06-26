<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left">
            <div class="bg-white rounded-lg p-5 text-center space-y-4">
                <div><img :src="user.get_avatar" class="rounded-full mx-auto"></div>
                <h2 class="font-bold text-lg">{{ user.name }}</h2>
                <div class="flex justify-around">
                    <div class="text-gray-500 text-xs">
                        <RouterLink :to="{ name: 'friends' }">{{ user.friends_count }} friends</RouterLink>
                    </div>
                    <div class="text-gray-500 text-xs">{{ user.posts_count }} posts</div>
                </div>
                <div>
                    <button :disabled="isrequestsent"
                        class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
                        :class="{ 'opacity-50 cursor-not-allowed': isrequestsent }" @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id">
                        {{ buttontext }}
                    </button>

                    <button class="inline-block mt-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
                        @click="sendDirectMessage" v-if="userStore.user.id !== user.id">
                        Send direct message
                    </button>

                    <RouterLink :to="{ name: 'editprofile', params: { id: $route.params.id } }"
                        class="inline-block mr-3 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
                        v-if="userStore.user.id === user.id">
                        Edit profile
                    </RouterLink>

                    <button class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" @click="logout"
                        v-if="userStore.user.id === user.id">
                        Log out
                    </button>

                </div>
            </div>
        </div>
        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg" v-if="userStore.user.id == user.id">

                <PostForm v-bind:user="user" :posts="posts"></PostForm>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <PostItem v-bind:post="post" />
            </div>

            <Paginator :has_previous="has_previous" :has_next="has_next" :total_pages="total_pages"
                :current_page="current_page" @getFeed="getFeed" />
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
import Paginator from '../components/Paginator.vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnowVue,
        TrendsVue,
        PostItem,
        PostForm,
        Paginator,
    },

    setup() {
        const userStore = useUserStore()
        const ToastStore = useToastStore()

        return {
            userStore,
            ToastStore
        }
    },

    data() {
        return {
            posts: [],
            user: {},
            body: '',
            isrequestsent: false,
            isfriend: false,
            buttontext: 'Send Friendship Request',
            url: null,
            has_previous: false,
            has_next: false,
            total_pages: 0,
            current_page: 0,
        }
    },

    mounted() {
        this.getFeed(1);

    },

    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed(1)
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        getFeed(page) {
            axios
                .get(`/api/post/profile/${this.$route.params.id}/?page=${page}`)
                .then(response => {
                    this.has_previous = response.data.has_previous;
                    this.has_next = response.data.has_next;
                    this.total_pages = response.data.total_pages;
                    this.current_page = response.data.current_page;

                    this.posts = response.data.posts;
                    this.user = response.data.user;
                    if (this.user.id !== this.userStore.user.id) {
                        this.checkStatus();
                    }

                })
                .catch(error => {
                    console.log('error', error);
                })
        },

        checkStatus() {
            // console.log('this.userStore.user.id', this.userStore.user.id)
            // console.log('this.user.id', this.user.id);
            if (this.userStore.user.id !== this.user.id) {
                axios
                    .get(`/api/friend/request/${this.$route.params.id}/`)
                    .then(response => {
                        console.log('status', response.data);

                        if (response.data.isFriend === 'true') {
                            this.isfriend = true
                            this.buttontext = 'You are already friends'
                        }

                        if (response.data.isSent === 'true') {
                            this.isrequestsent = true
                            this.buttontext = 'Request has been sent'
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },

        logout() {
            this.userStore.removeToken()
            this.$router.push('/login')
        },

        sendFriendshipRequest() {
            axios
                .post(`/api/friend/request/${this.$route.params.id}/`)
                .then(response => {
                    console.log(response.data);
                    if (response.data.message === 'request sent successfully') {
                        this.ToastStore.showToast(5000, 'request sent successfully', 'bg-green-500 text-white')
                        this.isrequestsent = true
                        this.buttontext = 'Request has been sent'
                    } else {
                        this.ToastStore.showToast(5000, 'request already sent', 'bg-red-500 text-white')
                    }
                })
                .catch(error => {
                    console.log(error);
                })
        },

        sendDirectMessage() {
            console.log('sendDirectMessage');
            axios
                .post('api/chat/', {
                    'send_to': this.$route.params.id
                })
                .then(response => {
                    console.log(response.data);
                    this.$router.push('/chat')
                    // this.$router.push({ path: '/chat', params: { pk: response.data.conversation.id } })
                })
                .catch(error => {
                    console.log(error);
                })


        }

    }
}

</script>

