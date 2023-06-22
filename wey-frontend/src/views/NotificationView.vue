<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white rounded-lg p-4">
                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="notification in notifications"
                    v-bind:key="notification.id" v-if="notifications.length">
                    {{ notification.body }}

                    <button class="underline" @click="readNotification(notification)">Read more</button>
                </div>

                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
                    You don't have any unread notifications!
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'notification',

    data() {
        return {
            notifications: [],
        }
    },

    mounted() {
        this.getNotifications();
    },

    methods: {
        getNotifications() {
            console.log('getNotifications');
            axios
                .get('api/notification/')
                .then(response => {
                    // console.log(response.data);
                    this.notifications = response.data;
                })
                .catch(err => {
                    console.log(err);
                })
        },

        async readNotification(notification) {
            console.log('readNotification', notification.id)

            await axios
                .post(`/api/notification/?pk=${notification.id}`)
                .then(response => {
                    console.log(response.data)

                    if (notification.type_of_notification == 'post_like' || notification.type_of_notification == 'post_comment') {
                        this.$router.push({ name: 'postdetail', params: { id: notification.post_id } })
                    } else {
                        this.$router.push({ name: 'friends', params: { id: notification.created_for_id } })
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}





</script>