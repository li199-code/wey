<template>
    <div class="mx-auto max-w-7xl grid grid-cols-2 gap-4">
        <div class="main-left cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12 space-y-8">
            <h2 class="text-2xl font-semibold">Edit Profile</h2>
            <p class="text-gray-500">Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                Lorem ipsum dolor sit
                mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.</p>
            <RouterLink :to="{ name: 'editpassword', params: { 'id': $route.params.id } }"
                class="underline font-bold text-lg">
                Change password
            </RouterLink>
        </div>
        <div class="main-right cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12">
            <form action="" class="space-y-5" v-on:submit.prevent="submitForm">
                <div>
                    <label>Name</label><br>
                    <input type="text" v-model="form.name" placeholder="Your full name"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>E-mail</label><br>
                    <input type="email" v-model="form.email" placeholder="Your e-mail address"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>Avatar</label><br>
                    <input type="file" ref="file" accept="image/*" v-on:change="previewImage">
                    <br>
                    <img v-if="previewUrl" :src="previewUrl" alt="Preview" style="max-width: 200px; max-height: 200px;">
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>


                <button type="submit" class="p-4 bg-purple-500 text-white rounded-lg">Save changes</button>



            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name
            },
            errors: [],
            previewUrl: '',
        }
    },

    methods: {
        previewImage(event) {
            const file = this.$refs.file.files[0];
            const reader = new FileReader();

            reader.onload = (event) => {
                this.previewUrl = event.target.result;
            };

            reader.readAsDataURL(file);
        },
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            console.log('editprofile', response.data);

                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar,
                            })

                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>
