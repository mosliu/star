import api from './index'
import type { ApiResponse, StarOperationRequest } from '@/types'

export const starsApi = {
  // Add stars to a child
  add: async (childId: number, data: StarOperationRequest): Promise<{ star_count: number }> => {
    try {
      const response = await api.post<ApiResponse<{ star_count: number }>>(
        `/children/${childId}/stars/add`,
        data
      )
      if (!response.data.data) {
        throw new Error('Failed to add stars')
      }
      return response.data.data
    } catch (error: any) {
      // Extract error messages from the backend response
      if (error.response?.data?.errors) {
        const errors = error.response.data.errors
        const errorMessages: string[] = []
        for (const field in errors) {
          if (Array.isArray(errors[field])) {
            errorMessages.push(...errors[field])
          }
        }
        if (errorMessages.length > 0) {
          throw new Error(errorMessages.join(', '))
        }
      }
      throw error
    }
  },

  // Subtract stars from a child
  subtract: async (childId: number, data: StarOperationRequest): Promise<{ star_count: number }> => {
    try {
      const response = await api.post<ApiResponse<{ star_count: number }>>(
        `/children/${childId}/stars/subtract`,
        data
      )
      if (!response.data.data) {
        throw new Error('Failed to subtract stars')
      }
      return response.data.data
    } catch (error: any) {
      // Extract error messages from the backend response
      if (error.response?.data?.errors) {
        const errors = error.response.data.errors
        const errorMessages: string[] = []
        for (const field in errors) {
          if (Array.isArray(errors[field])) {
            errorMessages.push(...errors[field])
          }
        }
        if (errorMessages.length > 0) {
          throw new Error(errorMessages.join(', '))
        }
      }
      throw error
    }
  },
}
