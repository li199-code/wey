<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1 space-y-2">
            <template v-for="conversation in conversations" :key="conversation.id">


                <div class="flex flex-col space-y-2 justify-between bg-white p-4 rounded-lg"
                    :class="{ 'border border-blue-300': conversation.id == currentConversation }">
                    <button @click="getMessages(conversation.id)" class="flex justify-between items-center text-xs">
                        <div class="flex items-center justify-between space-x-2">
                            <template v-for="user in conversation.users" v-bind:key="user.id">
                                <img v-if="user.id !== userStore.user.id" class="w-[40px] rounded-full"
                                    :src="user.get_avatar" alt="">
                                <p class="text-xs font-bold" v-if="user.id !== userStore.user.id">{{ user.name }}</p>
                            </template>
                        </div>
                        <span class="text-gray-400">{{ conversation.modified_at_formatted }} ago</span>
                    </button>
                </div>

            </template>
        </div>
        <div class="main-right col-span-3 space-y-4">
            <div class="bg-white rounded-lg p-3 space-y-2">
                <template v-for="message in messages" :key="message.id">
                    <div v-if="message.created_by.id == userStore.user.id"
                        class="flex justify-end items-start space-x-2 max-w-md ml-auto">
                        <div>
                            <div class="bg-indigo-700 text-white rounded-l-lg rounded-br-lg px-4 py-2">
                                {{ message.body }}
                            </div>
                            <span class="mt-1 text-sm text-gray-400">{{ message.created_at_formatted }} ago</span>
                        </div>
                        <img class="w-[40px] rounded-full" :src="message.created_by.get_avatar" alt="">
                    </div>

                    <div v-else class="flex justify-start items-start space-x-2 max-w-md mr-auto">
                        <img class="w-[40px] rounded-full" :src="message.created_by.get_avatar" alt="">
                        <div>
                            <div class="bg-gray-300 rounded-r-lg rounded-bl-lg px-4 py-2">
                                {{ message.body }}
                            </div>
                            <span class="mt-1 text-sm text-gray-400">{{ message.created_at_formatted }} ago</span>
                        </div>
                    </div>

                </template>


            </div>

            <div class="bg-white rounded-lg">
                <form v-on:submit.prevent="sendMessage(currentConversation)">

                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Say something..."></textarea>
                    </div>
                    <div class="p-4 border-t border-gray-100">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>

                </form>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
    name: 'chatview',
    components: {

    },
    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },

    mounted() {
        this.getConversationList();
    },

    data() {
        return {
            conversations: [],
            messages: [],
            currentConversation: '',
            body: '',
        }

    },

    methods: {
        getMessages(pk) {
            console.log('getMessages');
            axios
                .get(`api/chat/${pk}/`)
                .then(response => {
                    console.log(response.data.messages);
                    this.messages = response.data.messages;
                    this.currentConversation = pk;
                    console.log('this.currentConversation', this.currentConversation);

                })
                .catch(err => {
                    console.log(err);
                })
        },

        getConversationList() {
            console.log('getConversationList');
            axios
                .get('api/chat/')
                .then(response => {
                    this.conversations = response.data.conversations;
                    this.currentConversation = response.data.conversations[0].id
                    console.log('this.currentConversation', this.currentConversation);
                    this.getMessages(this.currentConversation)
                })
                .catch(err => {
                    console.log(err);
                })
        },



        sendMessage(pk) {
            console.log('sendMessage');
            axios
                .post(`api/chat/${pk}/`, { 'body': this.body })
                .then(response => {
                    console.log(response.data);
                    this.messages.push(response.data.message);
                    this.body = ''
                })
                .catch(err => {
                    console.log(err);
                })

        }


    },


}
</script>