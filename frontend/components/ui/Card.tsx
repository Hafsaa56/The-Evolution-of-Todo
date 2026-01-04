import { ReactNode } from 'react'

type CardProps = {
  children: ReactNode
  className?: string
}

export const Card = ({ children, className = '' }: CardProps) => {
  return (
    <div
      className={`bg-white shadow rounded-lg overflow-hidden ${className}`}
    >
      {children}
    </div>
  )
}

type CardHeaderProps = {
  children: ReactNode
  className?: string
}

export const CardHeader = ({ children, className = '' }: CardHeaderProps) => {
  return (
    <div className={`px-4 py-5 sm:px-6 border-b border-gray-200 ${className}`}>
      {children}
    </div>
  )
}

type CardBodyProps = {
  children: ReactNode
  className?: string
}

export const CardBody = ({ children, className = '' }: CardBodyProps) => {
  return <div className={`px-4 py-5 sm:p-6 ${className}`}>{children}</div>
}