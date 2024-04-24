import { Route, Routes } from "react-router-dom"
import { AppRoutes } from "../app/routes/AppRoutes"
// import { AuthRoutes } from "../auth/routes/AuthRoutes"
// import { CheckingAuth } from "../ui/components/CheckingAuth"
// import { useCheckAuth } from "../hooks"

export const AppRouter = () => {
    //   const status = useCheckAuth();;

    //   if (status === 'checking') {
    //     return <CheckingAuth />
    //   }

    return (
        <Routes>
            {/* {
        (status === 'authenticated')

          // Si esta autenticado pueden exisitr las Rutas App
          ? <Route path="/*" element={<AppRoutes />} />
          // Rutas registro y login
          : <Route path="/*" element={<AuthRoutes />} />
      } */}
            <Route path="/*" element={<AppRoutes />} />

        </Routes>
    )
}