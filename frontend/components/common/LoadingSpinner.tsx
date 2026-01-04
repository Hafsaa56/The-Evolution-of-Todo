type LoadingSpinnerProps = {
  size?: 'sm' | 'md' | 'lg'
}

export const LoadingSpinner = ({ size = 'md' }: LoadingSpinnerProps) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }

  return (
    <div className="flex justify-center items-center">
      <div
        className={`${sizeClasses[size]} animate-spin rounded-full border-t-2 border-b-2 border-indigo-600`}
      ></div>
    </div>
  )
}