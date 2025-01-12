import { Formik } from "formik";
import * as Yup from "yup";

const Login = () => {
  return (
    <div
      className="vw-100 vh-100 d-flex align-items-center justify-content-center"
      style={{ border: "2px red solid" }}
    >
      <Formik
        initialValues={{ email: "", password: "" }}
        validationSchema={Yup.object({
          password: Yup.string()
            .min(8, "Must be atleast 8 characters ")
            .required("Required"),
          email: Yup.string()
            .email("Invalid email address")
            .required("Required"),
        })}
        onSubmit={(values) => {
          console.log(values);
        }}
      >
        {(formik) => (
          <form
            onSubmit={formik.handleSubmit}
            className="d-flex align-items-center justify-content-center gap-4 flex-column "
          >
            <div>
              <input
                id="email"
                type="email"
                {...formik.getFieldProps("email")}
              />
              {formik.touched.email && formik.errors.email ? (
                <div>{formik.errors.email}</div>
              ) : null}
            </div>

            <div>
              <input
                id="password"
                type="text"
                {...formik.getFieldProps("password")}
              />
              {formik.touched.password && formik.errors.password ? (
                <div>{formik.errors.password}</div>
              ) : null}
            </div>

            <button type="submit">Submit</button>
          </form>
        )}
      </Formik>
    </div>
  );
};
export default Login;
