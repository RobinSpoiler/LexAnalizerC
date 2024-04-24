import { AppRouter } from "./router/AppRouter"
import { AppTheme } from "./app/theme"

export const App = () => {
  return (
    <AppTheme>
        <AppRouter/>
    </AppTheme>
  )
}