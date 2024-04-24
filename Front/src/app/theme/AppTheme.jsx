import { ThemeProvider } from "@emotion/react"
import CssBaseline from "@mui/material/CssBaseline"

import { theme } from "./"

export const AppTheme = ({children}) => {
  return (
    <ThemeProvider theme={theme}>
        <CssBaseline/>
        {children}
    </ThemeProvider>
  )
}